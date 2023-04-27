import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BookService } from '../services/book.service';
import { Book, Comment, Review } from '../models';

@Component({
  selector: 'app-book-detail',
  templateUrl: './book-detail.component.html',
  styleUrls: ['./book-detail.component.css']
})
export class BookDetailComponent implements OnInit {

  book: Book;
  loaded: boolean;
  comments: Comment[] = [];
  reviews: Review[] = [];
  viewComments: boolean = false;
  viewReviews: boolean = false;

  // bookReviews: 

  constructor(private route: ActivatedRoute, private bookService: BookService) { // ActivatedRoute is a injectable class, that's why we don't need to create instance with 'new'
    this.book = {} as Book;
    this.loaded = true;
  }
  
  ngOnInit(): void {
    this.getBookDetails()
  }

  getBookDetails() {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.route.paramMap.subscribe((params) => {
      const id = Number(params.get('id'));
      this.loaded = false;
      this.bookService.getBook(id).subscribe((book) => {
        this.book = book;
        this.loaded = true;
      })
    });
  }

  getComments(book: Book) {
    this.bookService.getBooksComments(this.book.id).subscribe((data: Comment[]) => {
      this.comments = data;
      this.viewComments = true;
    })
  }

  getReviews(book: Book) {
    this.bookService.getBooksReviews(this.book.id).subscribe((data: Review[]) => {
      this.reviews = data;
      this.viewReviews = true;
    })
  }

  // this.bookService.getCategories().subscribe((data: Category[]) => {
  //   this.categories = data;
  // })
}
