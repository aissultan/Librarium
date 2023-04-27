import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BookService } from '../services/book.service';
import { Book, Comment, Review } from '../models';
import { CommentService } from '../comment.service';
import { ReviewService } from '../review.service';


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
  extraBooks: Book[] = [];
  isExtraBooks: boolean = false;

  // For output comments and reviews
  isComments: boolean = false;
  isReviews: boolean = false;

  // For getting comment input
  comment: string = '';

  // For getting review input
  reviewComment: string = '';
  reviewRating: number = 0;

  constructor(private route: ActivatedRoute, private bookService: BookService, private commentService: CommentService, private reviewService: ReviewService) { // ActivatedRoute is a injectable class, that's why we don't need to create instance with 'new'
    this.book = {} as Book;
    this.loaded = true;
  }
  
  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.route.paramMap.subscribe((params) => {
      const id = Number(params.get('id'));
      this.loaded = false;
      this.bookService.getBook(id).subscribe((book) => {
        this.book = book;
        this.loaded = true;

        this.bookService.getBooksComments(this.book.id).subscribe((data: Comment[]) => {
          this.comments = data;
          this.isComments = this.comments.length > 0;
        })

        this.bookService.getBooksReviews(this.book.id).subscribe((data: Review[]) => {
          this.reviews = data;
          this.isReviews = this.reviews.length > 0;
        })

        this.bookService.getBooksByPublisher(this.book.publisher).subscribe((data: Book[]) => {
          this.extraBooks = data.filter(book => book.id !== this.book.id);
          // Если this.extraBooks не пустой, то присвоить isExtraBooks = True
          this.isExtraBooks = this.extraBooks.length > 0;
        })
      })
    });
  }

  submitReview() {
    this.reviewService.createReview(this.reviewComment, this.reviewRating).subscribe((data: Review) => {
      this.reviews.push(data);
      this.reviewComment = '';
    })
  }

  // rate(star: string) {
  //   const index = this.stars.indexOf(star);
  //   for(let i=0; i<5; i++) {
  //     if(i <= index) {
  //       this.stars[i] = 'star';
  //     } else {
  //       this.stars[i] = 'star_border';
  //     }
  //   }
  // }

  // writeComment() {
  //   this.commentService.writeComment(this.comment).subscribe((data: Comment) => {
  //     this.comments.push(data);
  //     this.comment = '';
  //   })
  // }
}
