import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DescargarVideo } from './descargar-video';

describe('DescargarVideo', () => {
  let component: DescargarVideo;
  let fixture: ComponentFixture<DescargarVideo>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DescargarVideo],
    }).compileComponents();

    fixture = TestBed.createComponent(DescargarVideo);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
