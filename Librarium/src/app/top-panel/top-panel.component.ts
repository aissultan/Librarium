import { Component, OnInit } from '@angular/core';
import { SignInComponent } from '../sign-in/sign-in.component';

@Component({
  selector: 'app-top-panel',
  templateUrl: './top-panel.component.html',
  styleUrls: ['./top-panel.component.css']
})
export class TopPanelComponent implements OnInit{
 logout(){
  localStorage.removeItem("token");
 }
 ngOnInit(): void {

 }
}
