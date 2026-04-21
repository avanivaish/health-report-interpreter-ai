import { Component, ChangeDetectorRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './upload.html',
  styleUrls: ['./upload.css']
})
export class UploadComponent {
  file: File | null = null;
  result: any = null;
  loading = false;

  constructor(
    private http: HttpClient,
    private cd: ChangeDetectorRef
  ) {}

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