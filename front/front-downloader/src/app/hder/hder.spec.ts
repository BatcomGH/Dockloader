import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Hder } from './hder';

describe('Hder', () => {
  let component: Hder;
  let fixture: ComponentFixture<Hder>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Hder],
    }).compileComponents();

    fixture = TestBed.createComponent(Hder);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
