import { Component, signal, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NgbToast } from '@ng-bootstrap/ng-bootstrap/toast';
import { MusicaService } from '../services/musica.service';

@Component({
  selector: 'app-descargar-musica',
  standalone: true,
  imports: [CommonModule, FormsModule, NgbToast],
  templateUrl: './descargar-musica.html',
  styleUrls: ['./descargar-musica.css']
})

export class DescargarMusicaComponent {
  videoUrl: string = '';
  cargando: boolean = false;
  mensajeError: string = '';
  readonly show = signal(true);

  constructor(private musicaService: MusicaService, private cdr: ChangeDetectorRef) {}

  descargar() {
    if (!this.videoUrl) return;

    this.cargando = true;
    this.mensajeError = '';

    this.musicaService.descargarMusica(this.videoUrl).subscribe({
      next: (response: any) => {
        // 1. Crear el objeto Blob
        const blob = new Blob([response.body], { type: response.body.type });

        // 2. Intentar extraer el nombre del archivo de los headers de Django
        const contentDisposition = response.headers.get('Content-Disposition');

        // Cuidado aquí: Como ahora descargas audios, tu fallback debería ser .mp3
        let filename = 'audio_descargado.mp3';
        if (contentDisposition) {
          const match = contentDisposition.match(/filename="?([^"]+)"?/);
          if (match && match.length === 2) filename = match[1];
        }

        // 3. Crear una URL temporal
        const downloadUrl = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = filename;

        // SOLUCIÓN 1: Pegar el enlace al DOM temporalmente (vital para Firefox/Safari)
        document.body.appendChild(link);

        link.click(); // Simulamos el clic

        // Limpiar el enlace del DOM inmediatamente
        document.body.removeChild(link);

        // SOLUCIÓN 2: Darle 100 milisegundos al navegador para que inicie la descarga
        // antes de destruir la URL de la memoria
        setTimeout(() => {
          window.URL.revokeObjectURL(downloadUrl);
        }, 100);

        this.videoUrl = '';
        this.cargando = false;
        this.cdr.detectChanges();
      },
      // Hacemos el callback asíncrono para leer el Blob fácilmente
      error: async (error) => {
        console.error('Detalle del error:', error);
        this.cargando = false;

        if (error.status === 0) {
          this.mensajeError = 'No se pudo conectar con el servidor. Posiblemente esté apagado.';
          this.cdr.detectChanges(); // <-- AVISAR A ANGULAR
          return;
        }

        if (error.error instanceof Blob) {
          try {
            const errorText = await error.error.text();
            const jsonError = JSON.parse(errorText);

            this.mensajeError = jsonError.error || jsonError.detail || jsonError.mensaje || 'Hubo un error interno en el servidor.';
            this.cdr.detectChanges(); // <-- AVISAR A ANGULAR
          } catch (e) {
            this.mensajeError = 'Hubo un error al procesar el video.';
            this.cdr.detectChanges(); // <-- AVISAR A ANGULAR
          }
        } else {
          this.mensajeError = error.error?.error || 'Error inesperado al intentar descargar.';
          this.cdr.detectChanges(); // <-- AVISAR A ANGULAR
        }
      }
    });
  }

  close() {
    this.show.set(false);
    setTimeout(() => this.show.set(true), 10000);
  }
}
