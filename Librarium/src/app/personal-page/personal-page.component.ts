import { Component, OnInit } from '@angular/core';


@Component({
  selector: 'app-personal-page',
  templateUrl: './personal-page.component.html',
  styleUrls: ['./personal-page.component.css']
})

export class PersonalPageComponent{
  name = 'John Smith';
  location = 'New York, NY';
  email = 'johnsmith@example.com';
  activeTab = 'books';

  setActiveTab(tab: string) {
    this.activeTab = tab;
  }
}
