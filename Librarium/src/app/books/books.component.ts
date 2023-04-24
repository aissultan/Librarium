import { Component, OnInit } from '@angular/core';
import { Book, Category } from '../models';
import { BookService } from '../services/book.service';

@Component({
  selector: 'app-books',
  templateUrl: './books.component.html',
  styleUrls: ['./books.component.css']
})
export class BooksComponent implements OnInit {
  books: Book[] = [];
  categories: Category[] = [];
  categoryBooks: Book[] = [];
  currentCategory: string = 'All';

  constructor(private bookService: BookService) {}

  ngOnInit(): void {
    this.bookService.getBooks().subscribe((data: Book[]) => {
      this.books = data;
      console.log(data)
    })

    this.bookService.getCategories().subscribe((data: Category[]) => {
      this.categories = data;
    })
  }

  getCategoryBooks(category: Category) {
    this.bookService.getCategoryBooks(category.id).subscribe((data: Book[]) => {
      this.categoryBooks = data;
      this.currentCategory = category.name;
    })
  }

  // getBook(book_id: number) {
  //   this.bookService.getBook(book_id).subscribe((data: Book) => {
  //     this. 
  //   })
  // }
}
