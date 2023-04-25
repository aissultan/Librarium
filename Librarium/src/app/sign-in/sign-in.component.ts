import { Component ,OnInit} from '@angular/core';
import { BookService } from '../services/book.service';
import { AuthToken } from '../models';

@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.css']
})
export class SignInComponent implements OnInit{
  logged : boolean = false;
  username : string = '';
  password : string = '';
  constructor(private bookService : BookService){

  }
  ngOnInit() {
    const token = localStorage.getItem('token');
    if(token){
    this.logged = true;
    }
  }
  login(){
    this.bookService.login(this.username,this.password).subscribe((data:AuthToken)=>{
      localStorage.setItem('token',data.token);
    this.logged = true;
      
    })
  }
  
}
