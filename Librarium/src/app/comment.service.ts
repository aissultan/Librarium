import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CommentService {

  BASE_URL = 'http://127.0.0.1:8000/api';

  constructor(private client: HttpClient) {}

  // writeComment(comment: string): Observable<Comment> {
  //   const now = new Date();
  //   return this.client.post<Comment>(`${this.BASE_URL}/comments/`, 
  //   {
  //     book: 
  //     user: 
  //     content: comment,
  //     date: now.toISOString()
  //   })
  // }

}
