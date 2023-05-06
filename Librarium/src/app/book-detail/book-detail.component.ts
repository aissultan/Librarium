import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BookService } from '../services/book.service';
import {Book, Comment, Review, SavedBook, User} from '../models';
import { CommentService } from '../comment.service';
import { ReviewService } from '../review.service';
import { LoginService } from '../services/login.service';
import { SavedBookService } from '../saved-book.service';


@Component({
  selector: 'app-book-detail',
  templateUrl: "./book-detail.component.html",
  styleUrls: ['./book-detail.component.css']
})
export class BookDetailComponent implements OnInit {
  user: User;
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

  // Update comment
  isUComment: boolean = false;
  updComment: string = '';

  // Update review
  isUReview: boolean = false;
  updReviewComment: string = '';
  updRating: number = 0;

  constructor(private route: ActivatedRoute, private bookService: BookService, private commentService: CommentService, private reviewService: ReviewService, private loginService: LoginService, private savedBookService: SavedBookService) { // ActivatedRoute is a injectable class, that's why we don't need to create instance with 'new'
    this.book = {} as Book;
    this.loaded = true;
    this.user = {} as User;

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

    this.loginService.getUser().subscribe(user => {
      this.user = user;
    });
  }

  submitReview() {
    this.reviewService.createReview(this.book.id, this.reviewComment, this.reviewRating).subscribe((data: Review) => {
      this.reviews.push(data);
      this.reviewComment = '';
    })
  }

  submitCommet() {
    this.commentService.writeComment(this.book.id, this.comment).subscribe((data: Comment) => {
      this.comments.push(data);
      this.comment = '';
    })
  }

  deleteComment(comment_id: number) {
    this.commentService.deleteComment(comment_id).subscribe((data: any) => {
      this.comments = this.comments.filter((comment) => comment.id !== comment_id)
    })
  }

  deleteReview(review_id: number) {
    this.reviewService.deleteReview(review_id).subscribe((data: any) => {
      this.reviews = this.reviews.filter((review) => review.id !== review_id)
    })
  }

  updateComment(comment_id: number) {
    this.commentService.updateComment(comment_id, this.book.id, this.updComment).subscribe((data: Comment) => {
      this.updComment = '';
      const index = this.comments.findIndex(comment => comment.id === data.id);
      if (index !== -1) {
        this.comments[index] = data;
      }
    })
  }

  updateReview(review_id: number) {
    this.reviewService.updateReview(review_id, this.book.id, this.updReviewComment, this.updRating).subscribe((data: any) => {
      this.updReviewComment = '';
      const index = this.reviews.findIndex(review => review.id === data.id);
      if (index !== -1) {
        this.reviews[index] = data;
      }
    })
  }

  setComment() {
    this.isUComment = !this.isUComment;
  }

  setReview() {
    this.isUReview = !this.isUReview;
    console.log(this.isUComment);
  }

  addToFavorites() {
    this.savedBookService.createSavedBook(this.book.id).subscribe((data: SavedBook) => {
      alert("Book was saved successfully!");
    })
  }
  
  readin(){
    window.open(`${this.book.link}`)
  }
}
