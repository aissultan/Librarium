import { Component, OnInit } from '@angular/core';
import { LoginService } from '../services/login.service';


@Component({
  selector: 'app-personal-page',
  templateUrl: './personal-page.component.html',
  styleUrls: ['./personal-page.component.css']
})

export class PersonalPageComponent implements OnInit{
  name:any;
  location = 'New York, NY';
  email = 'johnsmith@example.com';
  activeTab = 'books';
  constructor(private loginservice:LoginService){

  }
  setActiveTab(tab: string) {
    this.activeTab = tab;
  }
  ngOnInit(): void {
  this.loginservice.getUser()
  // if(localStorage.getItem('username')){
  console.log(localStorage.getItem('username'))
  
}
  
}
