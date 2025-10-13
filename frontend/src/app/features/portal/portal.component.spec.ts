import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PortalComponent } from '../../core/model/equipment.model';

describe('PortalComponent', () => {
  let component: PortalComponent;
  let fixture: ComponentFixture<PortalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PortalComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PortalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
