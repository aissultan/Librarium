import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Book, BookShelf } from '../models';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class BookshelfService {
  BASE_URL = 'http://127.0.0.1:8000/api';
  constructor(private client : HttpClient) { }
  getBookshelves(): Observable<BookShelf[]>{
    return this.client.get<BookShelf[]>(`${this.BASE_URL}/bookshelves/`)
  }
  createBookshelf(data: any){
    return this.client.post(`${this.BASE_URL}/bookshelf-create/`, data);
  }
  addBookToBookshelf(bookshelfId: number, book: Book): Observable<Book> {
    const url = `${this.BASE_URL}/bookshelves/${bookshelfId}/addbook/`;
    return this.client.post<Book>(url, book);
  }
  deleteBookshelf(bookshelfId:number):Observable<any>{
    return this.client.delete(`${this.BASE_URL}/bookshelves-delete/${bookshelfId}`)
  }
  deleteBook(bookshelfId: number, bookId: number): Observable<any> {
    return this.client.delete(`${this.BASE_URL}/bookshelves/${bookshelfId}/books/${bookId}`);
  }
}
