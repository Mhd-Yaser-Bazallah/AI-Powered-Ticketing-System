import { useTranslation } from 'react-i18next';

const Table = (props: any) => {
    const [t] = useTranslation();
    return (
        <div className="mt-5 panel p-0 border-0 text-center rounded-lg overflow-hidden">
            <div className="table-responsive  ">
                
                <table className="table-striped table-hover">
                    
                    <thead >
                        <tr >
                            {props.header.map((item: string,index:any) => (
                                <th className='text-left' key={index}>{item}</th>
                            ))}
                            <th className="!text-center">{t('Actions')}</th>
                        </tr>
                    </thead>
                    <tbody >{props.body}</tbody>
                </table>
            </div>
        </div>
    );
};

export default Table;
