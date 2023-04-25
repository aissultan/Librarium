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