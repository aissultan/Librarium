import { TestBed } from '@angular/core/testing';

import { FavBookService } from './favbook.service';

describe('FavBookService', () => {
  let service: FavBookService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FavBookService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
