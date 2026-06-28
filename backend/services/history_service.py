import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from pymongo import MongoClient
except ImportError:  # pragma: no cover - optional dependency
    MongoClient = None

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_HISTORY_PATH = BASE_DIR / "data" / "history.json"


class HistoryStore:
    def __init__(self, mongo_uri: Optional[str] = None, fallback_path: Optional[Path] = None):
        self.mongo_uri = mongo_uri or os.getenv("MONGO_URI", "")
        self.fallback_path = Path(fallback_path or DEFAULT_HISTORY_PATH)
        self._client = None
        self._collection = None

    def _connect(self):
        if self._collection is not None:
            return self._collection

        if self.mongo_uri and MongoClient is not None:
            try:
                self._client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=2000)
                self._client.admin.command("ping")
                db = self._client["health_report_ai"]
                self._collection = db["reports"]
                return self._collection
            except Exception:
                self._collection = None

        return None

    def _ensure_fallback_file(self) -> None:
        self.fallback_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.fallback_path.exists():
            self.fallback_path.write_text("[]", encoding="utf-8")

    def save_result(self, filename: str, result: Dict[str, Any]) -> Dict[str, Any]:
        entry = {
            "filename": filename,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "result": result,
        }

        collection = self._connect()
        if collection is not None:
            inserted = collection.insert_one(entry)
            entry["id"] = str(inserted.inserted_id)
            return entry

        self._ensure_fallback_file()
        history = json.loads(self.fallback_path.read_text(encoding="utf-8"))
        history.append(entry)
        self.fallback_path.write_text(json.dumps(history, indent=2), encoding="utf-8")
        entry["id"] = str(len(history))
        return entry

    def get_history(
        self, search_query: Optional[str] = None, risk_level: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        collection = self._connect()
        if collection is not None:
            query = {}
            if search_query:
                query["filename"] = {"$regex": search_query, "$options": "i"}
            if risk_level:
                query["result.risk_level"] = risk_level

            items = list(collection.find(query).sort("created_at", -1))
            return [
                {
                    "id": str(item.get("_id", "")),
                    "filename": item.get("filename", "Untitled"),
                    "created_at": item.get("created_at"),
                    "result": item.get("result", {}),
                }
                for item in items
            ]

        self._ensure_fallback_file()
        history = json.loads(self.fallback_path.read_text(encoding="utf-8"))
        items = reversed(history)

        if search_query:
            items = [
                item
                for item in items
                if search_query.lower() in item.get("filename", "").lower()
            ]
        if risk_level:
            items = [
                item for item in items if item.get("result", {}).get("risk_level") == risk_level
            ]

        return [
            {
                "id": str(index),
                "filename": item.get("filename", "Untitled"),
                "created_at": item.get("created_at"),
                "result": item.get("result", {}),
            }
            for index, item in enumerate(items)
        ]

    def get_report(self, report_id: str) -> Optional[Dict[str, Any]]:
        collection = self._connect()
        if collection is not None:
            from bson import ObjectId

            try:
                item = collection.find_one({"_id": ObjectId(report_id)})
                if item:
                    return {
                        "id": str(item.get("_id", "")),
                        "filename": item.get("filename", "Untitled"),
                        "created_at": item.get("created_at"),
                        "result": item.get("result", {}),
                    }
            except Exception:
                pass

        self._ensure_fallback_file()
        history = json.loads(self.fallback_path.read_text(encoding="utf-8"))
        try:
            index = int(report_id)
            items = list(reversed(history))
            if 0 <= index < len(items):
                item = items[index]
                return {
                    "id": report_id,
                    "filename": item.get("filename", "Untitled"),
                    "created_at": item.get("created_at"),
                    "result": item.get("result", {}),
                }
        except ValueError:
            pass

        return None

    def delete_report(self, report_id: str) -> bool:
        collection = self._connect()
        if collection is not None:
            from bson import ObjectId

            try:
                result = collection.delete_one({"_id": ObjectId(report_id)})
                return result.deleted_count > 0
            except Exception:
                pass

        self._ensure_fallback_file()
        history = json.loads(self.fallback_path.read_text(encoding="utf-8"))
        try:
            index = int(report_id)
            if 0 <= index < len(history):
                history.pop(index)
                self.fallback_path.write_text(
                    json.dumps(history, indent=2), encoding="utf-8"
                )
                return True
        except (ValueError, IndexError):
            pass

        return False
