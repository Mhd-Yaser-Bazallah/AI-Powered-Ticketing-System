// import React from 'react';

// interface NumberInputProps {
//     names: string[];
//     labels: string[];
//     formik: any;
//     type: string;
//     onChange : any
// }

// export const Input: React.FC<NumberInputProps> = ({ names, labels, formik, type ,onChange }) => {
//     return (
//         <>
//             {names.map((name, index) => (
//                 <div className="form-group mb-6" key={name}>
//                     <label htmlFor={name} className="block text-lg font-semibold text-gray-800">{labels[index]}</label>
//                     <input
//                         placeholder={`Enter the ${name}`}
//                         type={type}
//                         onChange={onChange}
//                         id={name}
//                         {...formik.getFieldProps(name)}
//                         onBlur={formik.handleBlur} 
//                         className={`${formik.touched[name] && formik.errors[name] ? 'border-dashed border-2 border-red-600' : ''} mt-2 block w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-600 transition duration-200 ease-in-out`}
//                     />
//                     {formik.touched[name] && formik.errors[name] ? (
//                         <span className="badge text-danger text-xs">
//                             {formik.errors[name]}
//                         </span>
//                     ) : null}
//                 </div>
//             ))}
//         </>
//     );
// };



import React from 'react';

interface InputProps {
    names: string[]; // Array of input names
    labels: string[]; // Array of input labels
    formik: any; // Formik instance for handling values, errors, etc.
    type: string; // Type of the input field
    onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void; // Optional custom onChange handler
}

export const Input: React.FC<InputProps> = ({ names, labels, formik, type, onChange }) => {
    return (
        <>
            {names.map((name, index) => (
                <div className="form-group mb-6" key={name}>
                    {/* Label */}
                    <label htmlFor={name} className="block text-lg font-semibold text-gray-800">
                        {labels[index]}
                    </label>

                    {/* Input */}
                    <input
                        id={name}
                        name={name}
                        type={type}
                        placeholder={`Enter ${labels[index]}`}
                        value={formik.values[name]} // Bind value from Formik
                        onChange={(event) => {
                            if (onChange) onChange(event); // Trigger custom onChange
                            formik.handleChange(event); // Trigger Formik's handleChange
                        }}
                        onBlur={formik.handleBlur} // Formik's blur handler
                        className={`mt-2 block w-full p-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-600 transition duration-200 ease-in-out ${
                            formik.touched[name] && formik.errors[name]
                                ? 'border-red-600'
                                : 'border-gray-300'
                        }`}
                    />

                    {/* Error Display */}
                    {formik.touched[name] && formik.errors[name] && (
                        <span className="text-red-600 text-xs">{formik.errors[name]}</span>
                    )}
                </div>
            ))}
        </>
    );
};
