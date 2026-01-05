import { AxiosError } from "axios";
import toast from "react-hot-toast";

export default class BackendError extends AxiosError {
    statusCode: number;
    message: any;

    constructor(statusCode: number, errorData: any) {
        super();
        this.statusCode = statusCode;
        console.log(this.message);
        
        // Extract all keys and create a concatenated error message
        if (typeof errorData === "string") {
            this.message = errorData; // If the error itself is a string
        } else if (typeof errorData === "object" && errorData !== null) {
            this.message = Object.keys(errorData)
                .map((key) => `${errorData[key]}`)
                .join(", "); // Construct a message from all keys
        } else {
            this.message = ""; // Default message
        }
    }

    errorMessage(): string | void {
        switch (this.statusCode) {
            case 404:
            case 400:
            case 401:
            case 402:
            case 403:
            case 422:
                return toast.error(this.message);
            case 500:
                return toast.error("Something Went Wrong. Try Again Later");
            default:
                return toast.error("Something Went Wrong");
        }
    }
}
