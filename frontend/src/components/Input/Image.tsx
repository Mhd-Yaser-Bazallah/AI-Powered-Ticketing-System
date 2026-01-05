import React from 'react';

interface ImageInputProps {
    names: string[];
    labels: string[];
    formik: any;
    previews: { [key: string]: string | null | any };
    handleFileChange: (event: React.ChangeEvent<HTMLInputElement>, field: string) => void;
}

export const ImageInput: React.FC<ImageInputProps> = ({ names, labels, formik, previews, handleFileChange }) => {
    return (
        <div className="grid sm:grid-cols-2 w-full gap-6 ">
            {names.map((name, index) => (
                <div className="form-group flex justify-center items-center flex-col mb-6" key={name}>
                    <label className="block  text-lg font-semibold text-gray-800">
                        {labels[index]}
                    </label>
                    <div className="relative w-40 h-40 mb-3 bg-gray-100 border border-gray-300 rounded-full overflow-hidden">
                        {previews[name] ? (
                            <img src={previews[name]} alt={`${name} Preview`} className="object-containe w-full h-full" />
                        ) : (
                            <div className="w-full h-full flex items-center justify-center text-gray-400">
                                No Image
                            </div>
                        )}
                    </div>
                    <input
                        id={name.toLowerCase()}
                        name={name}
                        type="file"
                        onChange={(event) => handleFileChange(event, name)}
                        className="hidden"
                        onBlur={formik.handleBlur}
                    />
                    <button
                        type="button"
                        onClick={() => document.getElementById(name.toLowerCase())?.click()}
                        className="btn bg-[#07054A] hover:bg-[#000] text-white mt-2 px-4 py-2"
                    >
                        Choose File
                    </button>
                    {formik.touched[name] && formik.errors[name] ? (
                        <span className="badge text-danger text-xs">
                            {formik.errors[name]}
                        </span>
                    ) : null}
                </div>
            ))}
        </div>
    );
};
