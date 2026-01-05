import React from 'react';

interface PaginationProps {
    currentPage: number;
    totalPages: number;
    onPageChange: (page: number) => void;
}

const Pagination = ({ currentPage, totalPages, onPageChange }: PaginationProps) => {
    const getPageNumbers = () => {
        const pages = [];
        const maxVisiblePages = 5; 
        if (totalPages > 0) pages.push(renderPageButton(1));
        let startPage = Math.max(2, currentPage - maxVisiblePages);
        let endPage = Math.min(totalPages - 1, currentPage + maxVisiblePages);
        if (currentPage <= maxVisiblePages + 1) {
            endPage = Math.min(totalPages - 1, maxVisiblePages + 1);
        } else if (currentPage >= totalPages - maxVisiblePages) {
            startPage = Math.max(2, totalPages - maxVisiblePages - 1);
        }
        if (startPage > 2) {
            pages.push(<span key="dots-start" className="flex items-center px-3">...</span>);
        }
        for (let i = startPage; i <= endPage; i++) {
            pages.push(renderPageButton(i));
        }
        if (endPage < totalPages - 1) {
            pages.push(<span key="dots-end" className="flex items-center px-3">...</span>);
        }
        if (totalPages > 1) pages.push(renderPageButton(totalPages));

        return pages;
    };

    const renderPageButton = (page: number) => (
        <button
            key={page}
            type="button"
            className={`flex justify-center font-semibold px-3.5 py-2 rounded-full transition ${
                currentPage === page
                    ? 'bg-[#43ADA5] text-white'
                    : 'bg-white-light text-dark hover:text-white hover:bg-[#000] dark:text-white-light dark:bg-[#191e3a] dark:hover:bg-primary'
            }`}
            onClick={() => onPageChange(page)}
        >
            {page}
        </button>
    );

    return (
        <nav className="flex justify-center space-x-2">
            {getPageNumbers()}
        </nav>
    );
};

export default Pagination;
