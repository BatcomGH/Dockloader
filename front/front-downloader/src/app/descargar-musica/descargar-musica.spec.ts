import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DescargarMusica } from './descargar-musica';

describe('DescargarMusica', () => {
  let component: DescargarMusica;
  let fixture: ComponentFixture<DescargarMusica>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DescargarMusica],
    }).compileComponents();

    fixture = TestBed.createComponent(DescargarMusica);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
