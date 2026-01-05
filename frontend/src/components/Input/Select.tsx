interface SelectInputProps {
    name: string;
    options: { [key: string]: any }[]; 
    formik: any;
    label: string;
    displayFields: string[]; 
}

export const SelectInput: React.FC<SelectInputProps> = ({ name, options, formik, label, displayFields }) => {
    return (
        <div className="form-group mb-6">
            <label htmlFor={name} className="block text-lg font-semibold text-gray-800">{label}</label>
            <select
                id={name}
                {...formik.getFieldProps(name)}
                className="mt-2 block w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-600 transition duration-200 ease-in-out"
            >
                <option value="" disabled>Select {label}</option>
                {options.map(option => (
                    <option key={option.id} value={option.id}>
                        {displayFields?.map(field => option[field] || '').join(' ')}
                    </option>
                ))}
            </select>
        </div>
    );
};
