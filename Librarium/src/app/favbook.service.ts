import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Book, FavBook } from './models';
import {map, Observable} from 'rxjs';
import { switchMap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})

export class FavBookService {

  BASE_URL = 'http://127.0.0.1:8000/';

  constructor(private client: HttpClient) {}

  addFavBook(book: Book, favbook: string): Observable<FavBook> {
    return this.client.post<FavBook>(`${this.BASE_URL}/favbook-create/`,
      {
        book: book,
        content: favbook,
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
