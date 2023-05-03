import { Component, OnInit } from '@angular/core';
import { User, FavBook } from '../models';
import { HttpClient } from '@angular/common/http';
import { LoginService } from '../services/login.service';
import { FavBookService } from '../favbook.service';

@Component({
  selector: 'app-personal-page',
  templateUrl: './personal-page.component.html',
  styleUrls: ['./personal-page.component.css']
})

export class PersonalPageComponent implements OnInit{
  user: User;
  favbook: FavBook[] = [];
  username: string | undefined;
  email: string | undefined;
  activeTab = 'books';
  constructor(private client: HttpClient, private loginService: LoginService, private favbookService: FavBookService) {
    this.user = {} as User;
  }


  ngOnInit() {

    this.loginService.getUser().subscribe(user => {
      this.user = user;
      this.username = user.username;
      this.email = user.email;
    });

  }
  setActiveTab(tab: string) {
    this.activeTab = tab;
  }



}
