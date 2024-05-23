/// <reference types="vite/client" />

declare module '*.(png|jpg|jpeg|gif|svg)' {
    const value: any;
    export default value;
  }
