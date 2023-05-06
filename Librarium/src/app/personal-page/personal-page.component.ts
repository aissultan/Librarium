import { Component, OnInit } from '@angular/core';
import { BookShelf, User } from '../models';
import { HttpClient } from '@angular/common/http';
import { LoginService } from '../services/login.service';
import { BookshelfService } from '../services/bookshelf.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-personal-page',
  templateUrl: './personal-page.component.html',
  styleUrls: ['./personal-page.component.css']
})

export class PersonalPageComponent {
  user: User;
  username: string | undefined;
  email: string | undefined;
  first_name: string | undefined;
  last_name:string | undefined;
  bookshelves: BookShelf[] = [];
  activeTab = 'books';
  edit: boolean = false;
  bookshelfEdit: boolean = false;
  selectedBookshelf: number | undefined;
  newNameBooksh :string = '';
  constructor(private http :HttpClient,private bookshelfService: BookshelfService, private loginService: LoginService) {
    this.user = {} as User;
  }

  ngOnInit() {
    this.bookshelfService.getBookshelves().subscribe((data:BookShelf[])=>{
      this.bookshelves = data;
    })
    this.loginService.getUser().subscribe(user => {
      this.user = user;
      this.username = user.username;
      this.email = user.email;
    });
  }
  addFirstSecondName(){
    this.http.put('http://127.0.0.1:8000/api/update-user/', {first_name: this.first_name, last_name: this.last_name}).subscribe(response => {
        console.log(response);
        this.user.first_name = this.first_name as string;
        this.user.last_name = this.last_name as string;
        this.edit = false;
        this.first_name = '';
        this.last_name = '';
    });
  }
  setActiveTab(tab: string) {
    this.activeTab = tab;
  }
  editting(){
    this.edit = true;

  }
  deleteBookshelf(bookshelf_id:number){
    this.bookshelfService.deleteBookshelf(bookshelf_id).subscribe((data:any)=>{
      this.bookshelves = this.bookshelves.filter((bookshelf)=>bookshelf.id !==bookshelf_id)
    })
  }
  openEdit(bookshelf_id : number){
    this.bookshelfEdit = true;    
    this.selectedBookshelf = bookshelf_id;
  }
  editBookshelf(bookshelf_id:number){
    console.log(bookshelf_id)
    const body = { name: this.newNameBooksh };
    this.http.put(`http://127.0.0.1:8000/api/bookshelves-update/${bookshelf_id}`,body).subscribe(
      response => console.log(response),
      error => console.log(error)
    )
    // updateComment(comment_id: number) { 
    //   this.commentService.updateComment(comment_id, this.book.id, this.updComment).subscribe((data: Comment) => { 
    //     this.updComment = ''; 
    //     const index = this.comments.findIndex(comment => comment.id === data.id); 
    //     if (index !== -1) { 
    //       this.comments[index] = data; 
    //     } 
    //   }) 
    // }
    const index = this.bookshelves.findIndex(bookshelf => bookshelf.id === bookshelf_id)
    this.bookshelves[index].name=this.newNameBooksh;
    this.newNameBooksh = '';
    this.bookshelfEdit = false;
    this.selectedBookshelf  = undefined;
  }
  deleteBook(bookshelfId : number, bookId: number): void {
    this.bookshelfService.deleteBook(bookshelfId, bookId)
      .subscribe(
        () => {
          // Handle success
        },
        (error) => {
          // Handle error
        }
      );
  }
}
