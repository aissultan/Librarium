import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { Observable } from 'rxjs';
import { AuthToken, Book, Category } from '../models';
import { Body } from '@angular/http/src/body';


@Injectable({
  providedIn: 'root'
})
export class BookService {
  BASE_URL = 'http://127.0.0.1:8000/api';

  constructor(private client: HttpClient) {}

  login(username : string, password : string): Observable<AuthToken>{
    return this.client.post<AuthToken>(
       `${this.BASE_URL}/login/`,
      {username,password}
    )
  }

  getCategories(): Observable<Category[]> {
    return this.client.get<Category[]>(`${this.BASE_URL}/categories/`)
  }

  getBooks(): Observable<Book[]> {
    return this.client.get<Book[]>(`${this.BASE_URL}/books/`)
  }

  getCategoryBooks(category_id: number): Observable<Book[]> {
    return this.client.get<Book[]>(`${this.BASE_URL}/categories/${category_id}/books/`)
  }

  getBook(book_id: number): Observable<Book> {
    return this.client.get<Book>(`${this.BASE_URL}/books/${book_id}`)
  }

  
}
