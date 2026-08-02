import { Routes } from '@angular/router';
import { DescargarVideoComponent } from './descargar-video/descargar-video';
import { DescargarAudioComponent } from './descargar-audio/descargar-audio';
import { DescargarMusicaComponent } from './descargar-musica/descargar-musica';

export const routes: Routes = [
  { path: '', redirectTo: '/video', pathMatch: 'full' },
  { path: 'video', component: DescargarVideoComponent },
  { path: 'musica', component: DescargarMusicaComponent },
  { path: 'audio', component: DescargarAudioComponent },
  { path: '**', redirectTo: '/video' }
];
