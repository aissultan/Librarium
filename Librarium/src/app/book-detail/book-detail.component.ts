import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BookService } from '../services/book.service';
import {Book, Comment, Review, User, BookShelf} from '../models';
import { CommentService } from '../comment.service';
import { ReviewService } from '../review.service';
import { BookshelfService } from '../services/bookshelf.service';
import { LoginService } from '../services/login.service';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-book-detail',
  templateUrl: "./book-detail.component.html",
  styleUrls: ['./book-detail.component.css']
})
export class BookDetailComponent implements OnInit {

  statusBookshelf : boolean;
  bookshelves : BookShelf[] = [];
  name : string ='';
  newNameBooksh :string = '';
  selectedBooks:number[] = [];
  user: User;
  book: Book;
  loaded: boolean;
  link : string;
  comments: Comment[] = [];
  reviews: Review[] = [];
  extraBooks: Book[] = [];
  isExtraBooks: boolean = false;
  edit: boolean = false;
  selectedBookshelf: number | undefined;
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
  liked: boolean = false;
  undoliked: boolean=false;

  updComment: string = '';
  likes: number;
  // Update review
  isUReview: boolean = false;
  updReviewComment: string = '';
  updRating: number = 0;

  constructor(private route: ActivatedRoute, private bookService: BookService, private commentService: CommentService,private bookshelfService : BookshelfService, private reviewService: ReviewService, private loginService: LoginService,
    private http: HttpClient) { // ActivatedRoute is a injectable class, that's why we don't need to create instance with 'new'
    this.book = {} as Book;
    this.statusBookshelf = false;
    this.loaded = true;
    this.link = '';
    this.likes = 0;
    this.user = {} as User;
    
  }

  ngOnInit(): void {

    this.bookshelfService.getBookshelves().subscribe((data:BookShelf[])=>{
      this.bookshelves = data;
    })


    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.route.paramMap.subscribe((params) => {
      const id = Number(params.get('id'));
      this.loaded = false;

      this.bookService.getBook(id).subscribe((book) => {
        this.book = book;
        this.loaded = true;
        this.link = book.link;
        this.likes = book.likes;

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

  addBookshelf() {
    this.statusBookshelf = true;
  }
  createBookshelf() {
    console.log(this.name,this.user.email)
    const body = {name : this.name, books : [this.book]};
    this.http.post('http://127.0.0.1:8000/api/bookshelf-create/', body).subscribe(
      response => {
        console.log(response);
        this.bookshelfService.getBookshelves().subscribe((data:BookShelf[])=>{
          this.bookshelves = data;
        })
        this.name = ''
      },
      error => {
        console.log(error);
      }
    );
  }
  addBook(bookshelf_id: number){
    this.bookshelfService.addBookToBookshelf(bookshelf_id,this.book).subscribe(
      response => {
        console.log(response);
        this.showMessage("Book added",2000)
      },
      error => {
        console.log(error);
      }
    )
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
  readin(){
    window.open(`${this.book.link}`)
  }
  telega(){
    console.log(this.book.link)
    window.open(`https://t.me/share/url?url=${this.book.link}&text=cool book let read it`)
  }
  whatsapp(){
    window.open(`https://wa.me/?text=YOUR_MESSAGE_HERE`)
  }
  insta(){
    window.open(`https://www.instagram.com/direct/new/?user={username}/url?url=${this.book.link}&text=wdew}`)
  }
  deleteBookshelf(bookshelf_id:number){
    this.bookshelfService.deleteBookshelf(bookshelf_id).subscribe((data:any)=>{
      this.bookshelves = this.bookshelves.filter((bookshelf)=>bookshelf.id !==bookshelf_id)
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
  openEdit(bookshelf_id : number){
    this.edit = true;
    this.selectedBookshelf = bookshelf_id;
  }
  editBookshelf(bookshelf_id:number){
    console.log(bookshelf_id)
    const body = { name: this.newNameBooksh };
    this.http.put(`http://127.0.0.1:8000/api/bookshelves-update/${bookshelf_id}`,body).subscribe(
      response => console.log(response),
      error => console.log(error)
    )
    this.edit = false;
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
  showMessage(message: string, duration: number) {
    // Создаем элемент div
    const div = document.createElement('div');
    div.textContent = message;
    div.style.position = 'fixed';
    div.style.top = '30%';
    div.style.left = '50%';
    div.style.transform = 'translateX(-50%)';
    div.style.padding = '12px';
    div.style.backgroundColor = '#333';
    div.style.color = '#fff';
    div.style.borderRadius = '6px';
    div.style.zIndex = '9999';
  
    // Добавляем элемент на страницу
    document.body.appendChild(div);
  
    // Через указанное время удаляем элемент
    setTimeout(() => {
      document.body.removeChild(div);
    }, duration);
  }
  

 

  likeBook() {
    if (!this.liked) {
      this.bookService.booklike(this.book.id).subscribe((data: Book) => {
        this.likes = data.likes;
        this.liked = true;
        this.undoliked=false;
      });
    }
  }

  undolikeBook() {
    if (!this.undoliked) {
      this.bookService.undobooklike(this.book.id).subscribe((data: Book) => {
        this.likes = data.likes;
        this.undoliked = true;
        this.liked = false;
      });
    }
  }



}
