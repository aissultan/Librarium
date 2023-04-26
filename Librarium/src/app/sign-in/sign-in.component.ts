import { Component ,OnInit} from '@angular/core';
import { AuthToken } from '../models';
import { LoginService } from '../services/login.service';

@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.css']
})
export class SignInComponent implements OnInit{
  logged : boolean = false;
  username : string = '';
  password : string = '';
  constructor(private loginService : LoginService){

  }
  ngOnInit() {
    const token = localStorage.getItem('token');
    if(token){
    this.logged = true;
    }
  }
  login(){
    this.loginService.login(this.username,this.password).subscribe((data:AuthToken)=>{
      localStorage.setItem('token',data.token);
      this.logged = true;
      
    })
  }
  
}
