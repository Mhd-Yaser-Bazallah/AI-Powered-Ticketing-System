import Skeleton from 'react-loading-skeleton';
import 'react-loading-skeleton/dist/skeleton.css';
const Button = () => {
    return (
        <>
            <div className="mb-4 text-end">
                <Skeleton width={'180px'} height={40} baseColor={localStorage.getItem('theme') === 'dark' ? '#0E1726' : ''} highlightColor={localStorage.getItem('theme') === 'dark' ? '#36454F' : ''} />
            </div>
        </>
    );
};

export default Button;
