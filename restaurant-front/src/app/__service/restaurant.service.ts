import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class RestaurantService {

  constructor(private http: HttpClient) { }

  baseUrl: string = "http://127.0.0.1:9002";

  getRestaurantList(data:any){
    return this.http.post<any>(this.baseUrl + '/home/rest/get-list/', data, {
      headers : new HttpHeaders()
    }).pipe(map((resp) => {
        return resp;
    }))
  }

  getLocationDetail(data:any){
    return this.http.get<any>(this.baseUrl + '/home/rest/get-location/', {
      headers : new HttpHeaders(),
      params: new HttpParams().append('rest_id', data)
    }).pipe(map((resp) => {
        return resp;
    }))
  }

}
