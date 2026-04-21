import { Component } from '@angular/core';
import { UploadComponent } from './upload/upload';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [UploadComponent],
  template: `<app-upload></app-upload>`
})
export class App {}