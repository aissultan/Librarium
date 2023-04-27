import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { LoginService } from '../services/login.service';
@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.css']
})

export class RegistrationComponent {
  email: string = '';
  username: string = '';
  password: string = '';
  confirmPassword: string = '';
  logged : boolean = false ;

  constructor(private http: HttpClient,private loginService : LoginService) {}

  register(){
    if  (this.password==this.confirmPassword){
      this.registerUser(this.email,this.username,this.password)
    }
    else {
      window.alert("Password are not the same")
    }
  }
  registerUser(email : string, username : string,password :string) {
    this.http.post('http://127.0.0.1:8000/api/register/',{email,username,password}).subscribe(
        (response) => {
          console.log('Registration successful.');
          this.logged = true;
        },
        (error) => {
          console.log('Registration failed.');
        }
      );
  }
}
