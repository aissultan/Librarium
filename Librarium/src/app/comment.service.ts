import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Book, Comment } from './models';
import {map, Observable} from 'rxjs';
import { switchMap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})

export class CommentService {

  BASE_URL = 'http://127.0.0.1:8000/';

  constructor(private client: HttpClient) {}

  writeComment(book: Book, comment: string): Observable<Comment> {
    const now = new Date();
    return this.client.post<Comment>(`${this.BASE_URL}/comments-create/`, 
    {
      book: book,
      content: comment,
      date: now.toISOString()
    })
  }

  // getComments() {
  //   return this.client.get<Comment[]>(`http://127.0.0.1:8000/api/comments/`).pipe(
  //     map(comments => {
  //       // Добавляем поле username к каждому комментарию
  //       return comments.map(comment => {
  //         const username = comment.user;
  //         return {
  //           ...comment,
  //           username
  //         };
  //       });
  //     })
  //   );
  // }
}
