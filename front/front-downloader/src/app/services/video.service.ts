import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class VideoService {
  private apiUrl = 'http://192.168.100.153:6767/api/descargar_video/';

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
