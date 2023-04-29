
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

export interface AuthToken{
    token : string;
}

export interface User {
    id: number;
    username: string;
    email: string;
    password: string;
}


export interface Review {
    id: number;
    book: Book;
    username: string;
    rating: number;
    comment: string;
}

export interface BookShelf {
    id: number;
    name: string;
    user: User;
    books: Book[];
}

export interface User {
    id: number;
    email: string;
    username: string;
    password: string;
    is_staff: boolean;
    is_superuser: boolean;
}  

export interface Comment {
    id: number;
    username: string;
    book: Book;
    content: string;
    date: Date;
}
