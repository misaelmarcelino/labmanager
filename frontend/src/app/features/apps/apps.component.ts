import { Component } from '@angular/core'
import { Router } from '@angular/router'

@Component({
  selector: 'app-apps',
  standalone: true,
  templateUrl: './apps.component.html',
  styleUrls: ['./apps.component.scss']
})
export class AppsComponent {

  constructor(private router: Router) {}

  openLabManager() {
    this.router.navigate(['/login'])
  }

  openStandin() {
    this.router.navigate(['/standin'])
  }

  openDS() {
    window.location.href = "http://ds-web"
  }

  openUpdateTracker() {
    window.location.href = "http://ds-web"
  }

  openVisionManager()  {
    window.location.href = "http://ds-web"
  }

}
