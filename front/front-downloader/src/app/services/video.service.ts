import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class VideoService {
  private apiUrl = environment.apiUrl + '/descargar_video/';

  constructor(private http: HttpClient) { }

  descargarVideo(url: string): Observable<any> {
    const body = { url: url };

    // ¡LÍNEA NUEVA! Forzamos a decirle al backend que le mandamos JSON
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });

    return this.http.post(this.apiUrl, body, {
      headers: headers, // Añadimos los headers a la petición
      responseType: 'blob',
      observe: 'response'
    });
  }
}
