import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { AuthToken } from '../models';

@Injectable({
  providedIn: 'root'
})
export class LoginService {
  BASE_URL = 'http://127.0.0.1:8000/api';
  private loggedStatus = new BehaviorSubject<boolean>(false);
  logged = this.loggedStatus.asObservable();

  constructor(private client: HttpClient) {}

  setStatus(newValue: boolean) {
    this.loggedStatus.next(newValue);
  }

  login(username : string, password : string): Observable<AuthToken>{
    return this.client.post<AuthToken>(
       `${this.BASE_URL}/login/`,
      {username,password}
    )
  }
  getUser() { 
    return this.client.get(this.BASE_URL + '/user/').subscribe((res: any) => {
      localStorage.setItem('username', res.username)
    }, error => {

    })
  }

}
