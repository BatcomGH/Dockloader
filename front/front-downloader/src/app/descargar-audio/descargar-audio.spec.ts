import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DescargarAudio } from './descargar-audio';

describe('DescargarAudio', () => {
  let component: DescargarAudio;
  let fixture: ComponentFixture<DescargarAudio>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DescargarAudio],
    }).compileComponents();

    fixture = TestBed.createComponent(DescargarAudio);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
