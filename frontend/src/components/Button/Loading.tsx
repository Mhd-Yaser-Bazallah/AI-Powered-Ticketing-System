import React from 'react'
import { useTranslation } from 'react-i18next'

const Loading = ({mutation , title}:any) => {
    const {t} = useTranslation()
    return (
        <>
            <button
                type="submit"
                disabled={mutation}
                className="btn bg-[#07054A] hover:bg-[#07054ab9] text-white w-full py-2 rounded-md shadow-lg transition duration-200">
                {mutation ? (
                    <>
                        <span className="animate-spin border-2 border-white border-l-transparent rounded-full w-5 h-5 mr-2 inline-block align-middle"></span>
                        {t('Loading')}...
                    </>
                ) : (
                    title
                )}
            </button>
        </>
    )
}

export default Loading