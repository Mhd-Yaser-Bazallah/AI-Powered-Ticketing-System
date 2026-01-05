import Skeleton from 'react-loading-skeleton';
import 'react-loading-skeleton/dist/skeleton.css';
const Table = () => {
    return (
        <>
            <Skeleton
                width={'100%'}
                className="h-[60vh] mt-5"
                baseColor={localStorage.getItem('theme') === 'dark' ? '#0E1726' : ''}
                highlightColor={localStorage.getItem('theme') === 'dark' ? '#36454F' : ''}
            />
        </>
    );
};

export default Table;
