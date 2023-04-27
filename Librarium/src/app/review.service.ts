import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Review } from './models';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ReviewService {

  BASE_URL = 'http://127.0.0.1:8000/api';

  constructor(private client: HttpClient) { }

  // submitReview() {
  //   this.reviewService.createReview(this.reviewComment, this.reviewRating).subscribe((data: Review) => {
  //     this.reviews.push(data);
  //     this.reviewComment = '';
  //   })
  // }

  createReview(reviewComment: string, reviewRating: number): Observable<Review> {
    return this.client.post<Review>(`${this.BASE_URL}/reviews/`, 
    {
      
    })
  }
}
