import { useMemo, useState } from 'react'
import './App.css'

const initialDrinks = [
  {
    id: 1,
    name: 'Кола',
    category: 'Газированные напитки',
    type: 'Газированный напиток',
    brand: 'Classic Cola',
    tags: ['сладкий', 'газированный', 'холодный'],
    description: 'Классический газированный напиток с насыщенным вкусом.',
    available: true,
  },
  {
    id: 2,
    name: 'Апельсиновый сок',
    category: 'Соки',
    type: 'Фруктовый сок',
    brand: 'Fresh Orange',
    tags: ['апельсин', 'фруктовый', 'сок'],
    description: 'Освежающий апельсиновый сок с ярким фруктовым вкусом.',
    available: true,
  },
  {
    id: 3,
    name: 'Минеральная вода',
    category: 'Вода',
    type: 'Минеральная вода',
    brand: 'Aqua',
    tags: ['вода', 'минеральный'],
    description: 'Минеральная вода для ежедневного употребления.',
    available: true,
  },
  {
    id: 4,
    name: 'Холодный чай',
    category: 'Чай',
    type: 'Холодный чай',
    brand: 'Ice Tea',
    tags: ['чай', 'холодный', 'лимон'],
    description: 'Холодный чай с лёгким лимонным вкусом.',
    available: false,
  },
  {
    id: 5,
    name: 'Яблочный сок',
    category: 'Соки',
    type: 'Фруктовый сок',
    brand: 'Apple Fresh',
    tags: ['яблоко', 'фруктовый', 'сок'],
    description: 'Натуральный яблочный сок с мягким фруктовым вкусом.',
    available: true,
  },
  {
    id: 6,
    name: 'Лимонад',
    category: 'Газированные напитки',
    type: 'Лимонад',
    brand: 'Fresh Lemon',
    tags: ['лимон', 'газированный', 'сладкий'],
    description: 'Освежающий лимонад с выраженным цитрусовым вкусом.',
    available: true,
  },
]

const categories = [
  'Газированные напитки',
  'Соки',
  'Вода',
  'Чай',
]

const tags = [
  'сладкий',
  'газированный',
  'холодный',
  'сок',
  'фруктовый',
  'лимон',
  'вода',
]

function Header() {
  return (
    <header className="header">
      <div className="header__content">
        <p className="header__subtitle">КАТАЛОГ НАПИТКОВ</p>
        <h1>Drink Catalog</h1>
        <p className="header__description">
          React-версия каталога напитков без серверной части
        </p>
      </div>
    </header>
  )
}

function Sidebar({
  selectedCategory,
  selectedTag,
  onCategorySelect,
  onTagSelect,
  onResetFilters,
}) {
  return (
    <aside className="sidebar">
      <div className="sidebar__block">
        <h2>Категории</h2>

        <button
          className={
            selectedCategory === 'all'
              ? 'sidebar__link sidebar__link_active'
              : 'sidebar__link'
          }
          type="button"
          onClick={onResetFilters}
        >
          Все категории
        </button>

        {categories.map((category) => (
          <button
            className={
              selectedCategory === category
                ? 'sidebar__link sidebar__link_active'
                : 'sidebar__link'
            }
            type="button"
            key={category}
            onClick={() => onCategorySelect(category)}
          >
            {category}
          </button>
        ))}
      </div>

      <div className="sidebar__block">
        <h2>Теги</h2>

        <div className="tags">
          {tags.map((tag) => (
            <button
              className={
                selectedTag === tag
                  ? 'tag tag_active'
                  : 'tag'
              }
              type="button"
              key={tag}
              onClick={() => onTagSelect(tag)}
            >
              {tag}
            </button>
          ))}
        </div>
      </div>

      {(selectedCategory !== 'all' || selectedTag !== 'all') && (
        <button
          className="reset-button"
          type="button"
          onClick={onResetFilters}
        >
          Сбросить фильтры
        </button>
      )}
    </aside>
  )
}

function SortPanel({ sortBy, onSortChange }) {
  return (
    <div className="sort-preview">
      <label htmlFor="sort">Сортировка</label>

      <select
        id="sort"
        value={sortBy}
        onChange={(event) => onSortChange(event.target.value)}
      >
        <option value="newest">Сначала новые</option>
        <option value="name">По названию</option>
        <option value="category">По категории</option>
        <option value="brand">По бренду</option>
      </select>
    </div>
  )
}

function DrinkCard({ drink }) {
  return (
    <article className="drink-card">
      <div className="drink-card__image">
        <span>{drink.name[0]}</span>
      </div>

      <div className="drink-card__body">
        <div className="drink-card__title-row">
          <h3>{drink.name}</h3>

          <span
            className={
              drink.available
                ? 'status status_available'
                : 'status status_unavailable'
            }
          >
            {drink.available ? 'В наличии' : 'Нет в наличии'}
          </span>
        </div>

        <p>
          <strong>Категория:</strong> {drink.category}
        </p>

        <p>
          <strong>Тип:</strong> {drink.type}
        </p>

        <p>
          <strong>Бренд:</strong> {drink.brand}
        </p>

        <p className="drink-card__description">
          {drink.description}
        </p>

        <div className="drink-card__tags">
          {drink.tags.map((tag) => (
            <span
              className="drink-tag"
              key={tag}
            >
              {tag}
            </span>
          ))}
        </div>

        <div className="drink-card__actions">
          <button
            className="button button_primary"
            type="button"
          >
            Открыть
          </button>

          <button
            className="button"
            type="button"
          >
            Редактировать
          </button>

          <button
            className="button button_danger"
            type="button"
          >
            Удалить
          </button>
        </div>
      </div>
    </article>
  )
}

function DrinkList({ drinks }) {
  if (drinks.length === 0) {
    return (
      <div className="empty-message">
        Напитки по выбранному фильтру не найдены.
      </div>
    )
  }

  return (
    <div className="drink-grid">
      {drinks.map((drink) => (
        <DrinkCard
          drink={drink}
          key={drink.id}
        />
      ))}
    </div>
  )
}

function App() {
  const [sortBy, setSortBy] = useState('newest')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [selectedTag, setSelectedTag] = useState('all')

  const visibleDrinks = useMemo(() => {
    let result = [...initialDrinks]

    if (selectedCategory !== 'all') {
      result = result.filter(
        (drink) => drink.category === selectedCategory,
      )
    }

    if (selectedTag !== 'all') {
      result = result.filter(
        (drink) => drink.tags.includes(selectedTag),
      )
    }

    if (sortBy === 'name') {
      result.sort((a, b) =>
        a.name.localeCompare(b.name, 'ru'),
      )
    }

    if (sortBy === 'category') {
      result.sort((a, b) =>
        a.category.localeCompare(b.category, 'ru'),
      )
    }

    if (sortBy === 'brand') {
      result.sort((a, b) =>
        a.brand.localeCompare(b.brand, 'ru'),
      )
    }

    if (sortBy === 'newest') {
      result.sort((a, b) => b.id - a.id)
    }

    return result
  }, [sortBy, selectedCategory, selectedTag])

  function handleCategorySelect(category) {
    setSelectedCategory(category)
    setSelectedTag('all')
  }

  function handleTagSelect(tag) {
    setSelectedTag(tag)
    setSelectedCategory('all')
  }

  function handleResetFilters() {
    setSelectedCategory('all')
    setSelectedTag('all')
  }

  return (
    <div className="app">
      <Header />

      <main className="layout">
        <Sidebar
          selectedCategory={selectedCategory}
          selectedTag={selectedTag}
          onCategorySelect={handleCategorySelect}
          onTagSelect={handleTagSelect}
          onResetFilters={handleResetFilters}
        />

        <section className="content">
          <div className="content__header">
            <div>
              <h2>Каталог напитков</h2>

              <p>
                Найдено напитков: {visibleDrinks.length}
              </p>
            </div>

            <SortPanel
              sortBy={sortBy}
              onSortChange={setSortBy}
            />
          </div>

          <DrinkList drinks={visibleDrinks} />
        </section>
      </main>
    </div>
  )
}

export default App