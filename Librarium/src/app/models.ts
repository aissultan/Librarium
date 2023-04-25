export interface Book {
    id: number;
    title: string;
    author: string; 
    year: number;
    publisher: string;
    image: string;
    description: string;
    category: Category;
    rating: number;
}

export interface Category {
    id: number; 
    name: string;
}

export interface User {
    id: number;
    name: string;
    email: string;
    password: string;
}

export interface Review {
    id: number;
    book: Book;
    user: User;
    rating: number;
    comment: string;
}

export interface BookShelf {
    id: number;
    name: string;
    user: User;
    books: Book[];
}

export interface Comment {
    id: number;
    book: Book;
    user: User;
    content: string;
    date: Date;
}