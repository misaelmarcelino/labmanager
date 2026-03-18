import { Component } from '@angular/core'
import { ApiService } from '../../core/services/api.service'
import { CommonModule } from '@angular/common'
import { HeaderComponent } from '../../shared/header/header.component'
import { interval, Subscription } from 'rxjs'

@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [CommonModule, HeaderComponent],
  templateUrl: './upload.component.html',
  styleUrl: './upload.component.scss'
})
export class UploadComponent {

  selectedFile: File | null = null

  loading = false
  result: any = null

  jobId: string | null = null
  status: string = ''
  steps: string[] = []

  pollSub!: Subscription

  constructor(private api: ApiService) {}

  onFileSelected(event: any) {

    const file = event.target.files[0]

    if (file) {
      this.selectedFile = file
    }

  }

  upload() {

    if (!this.selectedFile) return

    this.loading = true
    this.result = null
    this.steps = []

    this.api.uploadFile(this.selectedFile)
      .subscribe({

        next: (response: any) => {

          this.jobId = response.job_id

          this.startPolling(this.jobId!)

          this.selectedFile = null

          const input = document.querySelector('input[type=file]') as HTMLInputElement
          if (input) input.value = ''

        },

        error: (err) => {

          console.error(err)
          this.loading = false

        }

      })

  }

  startPolling(job_id: string) {

    this.pollSub = interval(1000).subscribe(() => {

      this.api.getStatus(job_id).subscribe((res: any) => {

        this.steps = res.steps
        this.status = res.status
        this.result = res.result

        if (res.finished) {

          this.pollSub.unsubscribe()
          this.loading = false

        }

      })

    })

  }

}
