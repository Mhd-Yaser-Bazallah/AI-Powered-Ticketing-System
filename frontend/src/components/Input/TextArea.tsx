import React from 'react';

export const TextArea = ({ name, label, formik, placeholder }: any) => {
    const error = formik.touched[name] && formik.errors[name];

    return (
        <div className="w-full">
            {label && <label htmlFor={name} className="block text-lg font-semibold text-gray-800">{label}</label>}
            <textarea
                id={name}
                name={name}
                rows={4}
                placeholder={placeholder}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values[name]}
                className={`block w-full rounded-md border ${
                    error ? 'border-red-500' : 'border-gray-300'
                } shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm`}
            />
            {error && <p className="text-red-500 text-xs mt-1">{error}</p>}
        </div>
    );
};
