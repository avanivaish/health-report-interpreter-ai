import { Component, ChangeDetectorRef, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './upload.html',
  styleUrls: ['./upload.css']
})
export class UploadComponent implements OnInit {
  file: File | null = null;
  result: any = null;
  loading = false;
  history: any[] = [];
  searchQuery = '';
  selectedRisk: string = '';
  viewingReportId: string | null = null;
  compareMode = false;
  compareIds: Set<string> = new Set();
  compare1: any = null;
  compare2: any = null;

  constructor(
    private http: HttpClient,
    private cd: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.loadHistory();
  }

  loadHistory() {
    const params = new URLSearchParams();
    if (this.searchQuery) params.append('search', this.searchQuery);
    if (this.selectedRisk) params.append('risk_level', this.selectedRisk);
    const url = `http://127.0.0.1:8000/history?${params.toString()}`;

    this.http.get(url).subscribe({
      next: (res: any) => {
        this.history = Array.isArray(res) ? res : [];
        this.cd.detectChanges();
      },
      error: () => {
        this.history = [];
      }
    });
  }

  onSearchChange() {
    this.loadHistory();
  }

  onRiskFilterChange() {
    this.loadHistory();
  }

  viewReport(reportId: string) {
    this.http.get(`http://127.0.0.1:8000/report/${reportId}`).subscribe({
      next: (res: any) => {
        this.result = res;
        this.viewingReportId = reportId;
        this.cd.detectChanges();
      },
      error: () => alert('Failed to load report')
    });
  }

  deleteReport(reportId: string, event: Event) {
    event.stopPropagation();
    if (!confirm('Delete this report?')) return;

    this.http.delete(`http://127.0.0.1:8000/report/${reportId}`).subscribe({
      next: () => {
        this.loadHistory();
        this.cd.detectChanges();
      },
      error: () => alert('Failed to delete report')
    });
  }

  toggleCompare(reportId: string, event: Event) {
    event.stopPropagation();
    if (this.compareIds.has(reportId)) {
      this.compareIds.delete(reportId);
    } else if (this.compareIds.size < 2) {
      this.compareIds.add(reportId);
    }
    if (this.compareIds.size === 2) {
      this.loadCompareReports();
    }
    this.cd.detectChanges();
  }

  loadCompareReports() {
    const ids = Array.from(this.compareIds);
    this.compare1 = null;
    this.compare2 = null;

    if (ids[0]) {
      this.http.get(`http://127.0.0.1:8000/report/${ids[0]}`).subscribe({
        next: (res: any) => {
          this.compare1 = res;
          this.cd.detectChanges();
        }
      });
    }

    if (ids[1]) {
      this.http.get(`http://127.0.0.1:8000/report/${ids[1]}`).subscribe({
        next: (res: any) => {
          this.compare2 = res;
          this.cd.detectChanges();
        }
      });
    }
  }

  exportReport(reportId: string, format: string, event: Event) {
    event.stopPropagation();
    const url = `http://127.0.0.1:8000/report/${reportId}/export?format=${format}`;

    if (format === 'json') {
      this.http.get(url).subscribe({
        next: (data: any) => {
          const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
          const link = document.createElement('a');
          link.href = URL.createObjectURL(blob);
          link.download = `${reportId}.json`;
          link.click();
        }
      });
    } else if (format === 'pdf') {
      window.open(url, '_blank');
    }
  }

  closeCompare() {
    this.compareIds.clear();
    this.compare1 = null;
    this.compare2 = null;
    this.cd.detectChanges();
  }

  isSelected(reportId: string): boolean {
    return this.compareIds.has(reportId);
  }

  // 📁 File select
  onFileSelected(event: any) {
    if (event.target.files.length > 0) {
      this.file = event.target.files[0];
    }
  }

  // 🔥 Drag over (required to allow drop)
  onDragOver(event: DragEvent) {
    event.preventDefault();
  }

  // 🔥 Handle file drop
  onDrop(event: DragEvent) {
    event.preventDefault();

    if (event.dataTransfer?.files.length) {
      this.file = event.dataTransfer.files[0];
      this.cd.detectChanges(); // update UI instantly
    }
  }

  // 🚀 Upload logic
  upload() {
    if (!this.file) {
      alert('Select a file first');
      return;
    }

    const formData = new FormData();
    formData.append('file', this.file);

    this.loading = true;
    this.result = null; // 🔥 clear previous result

    this.http.post('http://127.0.0.1:8000/upload', formData)
      .subscribe({
        next: (res: any) => {
          console.log("API RESPONSE:", res);

          this.result = res;
          this.loading = false;
          this.loadHistory();

          this.cd.detectChanges();
        },
        error: (err) => {
          console.error("ERROR:", err);

          this.loading = false;
          this.cd.detectChanges();

          alert('Upload failed');
        }
      });
  }
}