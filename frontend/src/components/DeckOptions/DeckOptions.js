import React, { useState, useEffect } from 'react'
import './DeckOptions.css'

const DeckOptions = ({ onSetSortOption, sortOption }) => {

    const [sortMenuActive, setSortMenuActive] = useState(false);

    const handleToggleSortMenu = () => setSortMenuActive(active => !active);

    const handleSetSortOption = (option) => {
        onSetSortOption(option);
        setSortMenuActive(false);
    }
    

    return (
        <div className="deck-options">
            <div className="option-container">
                <div className="option-header" onClick={handleToggleSortMenu}>Sort</div>
                {sortMenuActive && (
                    <SortOption 
                        onSetSortOption={handleSetSortOption} 
                        sortOption={sortOption}
                    />
                )}
            </div>
            {/* Placeholder for future options */}
        </div>
    )
}

const SortOption = ({ onSetSortOption, sortOption }) => {

    const handleSetSortOption = (option) => {
        if (option !== sortOption) {
            onSetSortOption(option);
        }
    }

    const getClassName = (option) => {
        return `dropdown-sort-item ${sortOption === option ? 'active' : '' }`
    }

    return (
        <div className="dropdown-sort">
            <div className={getClassName('last-updated')} id='last-updated' onClick={e => handleSetSortOption(e.target.id)}>Last Updated</div>
            <div className={getClassName('newest')} id='newest' onClick={e => handleSetSortOption(e.target.id)}>Newest</div>
            <div className={getClassName('oldest')} id='oldest' onClick={e => handleSetSortOption(e.target.id)}>Oldest</div>
        </div>
    )
}

export default DeckOptions;