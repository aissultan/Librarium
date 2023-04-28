import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import {map, Observable} from 'rxjs';
import { Comment, User } from './models';
import { switchMap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class CommentService {

  BASE_URL = 'http://127.0.0.1:8000/';

  constructor(private client: HttpClient) { }

  getComments() {
    return this.client.get<Comment[]>(`http://127.0.0.1:8000/api/comments/`).pipe(
      map(comments => {
        // Добавляем поле username к каждому комментарию
        return comments.map(comment => {
          const username = comment.user.name;
          return {
            ...comment,
            username
          };
        });
      })
    );
  }
}
