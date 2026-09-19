import { useEffect, useMemo, useState } from 'react'
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
    image: '',
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
    image: '',
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
    image: '',
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
    image: '',
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
    image: '',
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
    image: '',
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

const emptyFormData = {
  name: '',
  category: '',
  type: '',
  brand: '',
  tags: '',
  description: '',
  image: '',
  available: true,
}

function getSavedDrinks() {
  try {
    const savedDrinks = localStorage.getItem('drink-catalog-drinks')

    return savedDrinks
      ? JSON.parse(savedDrinks)
      : initialDrinks
  } catch {
    return initialDrinks
  }
}

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

function DrinkForm({
  formData,
  errors,
  isEditing,
  onInputChange,
  onSubmit,
  onCancelEdit,
}) {
  return (
    <section className="drink-form">
      <div className="drink-form__header">
        <div>
          <h2>
            {isEditing
              ? 'Редактирование напитка'
              : 'Добавление напитка'}
          </h2>

          <p>
            {isEditing
              ? 'Измените необходимые данные'
              : 'Заполните данные нового напитка'}
          </p>
        </div>
      </div>

      <form onSubmit={onSubmit} noValidate>
        <div className="form-grid">
          <div className="form-group">
            <label htmlFor="name">Название</label>

            <input
              id="name"
              name="name"
              type="text"
              value={formData.name}
              onChange={onInputChange}
              className={errors.name ? 'field field_error' : 'field'}
              placeholder="Например, Имбирный лимонад"
            />

            {errors.name && (
              <span className="error-message">
                {errors.name}
              </span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="category">Категория</label>

            <select
              id="category"
              name="category"
              value={formData.category}
              onChange={onInputChange}
              className={
                errors.category
                  ? 'field field_error'
                  : 'field'
              }
            >
              <option value="">Выберите категорию</option>

              {categories.map((category) => (
                <option value={category} key={category}>
                  {category}
                </option>
              ))}
            </select>

            {errors.category && (
              <span className="error-message">
                {errors.category}
              </span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="type">Тип напитка</label>

            <input
              id="type"
              name="type"
              type="text"
              value={formData.type}
              onChange={onInputChange}
              className={errors.type ? 'field field_error' : 'field'}
              placeholder="Например, Лимонад"
            />

            {errors.type && (
              <span className="error-message">
                {errors.type}
              </span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="brand">Бренд</label>

            <input
              id="brand"
              name="brand"
              type="text"
              value={formData.brand}
              onChange={onInputChange}
              className={errors.brand ? 'field field_error' : 'field'}
              placeholder="Например, Ginger Fresh"
            />

            {errors.brand && (
              <span className="error-message">
                {errors.brand}
              </span>
            )}
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="tags">
            Теги через запятую
          </label>

          <input
            id="tags"
            name="tags"
            type="text"
            value={formData.tags}
            onChange={onInputChange}
            className="field"
            placeholder="имбирь, лимон, газированный"
          />
        </div>

        <div className="form-group">
          <label htmlFor="image">Изображение</label>

          <input
            id="image"
            name="image"
            type="file"
            accept="image/*"
            onChange={onInputChange}
            className="field"
          />

          {formData.image && (
            <div className="image-preview">
              <img
                src={formData.image}
                alt="Предпросмотр напитка"
              />
            </div>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="description">Описание</label>

          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={onInputChange}
            className={
              errors.description
                ? 'field field_error form-textarea'
                : 'field form-textarea'
            }
            placeholder="Описание напитка"
          />

          {errors.description && (
            <span className="error-message">
              {errors.description}
            </span>
          )}
        </div>

        <label className="checkbox-field">
          <input
            name="available"
            type="checkbox"
            checked={formData.available}
            onChange={onInputChange}
          />

          <span>Напиток в наличии</span>
        </label>

        <div className="form-actions">
          <button
            className="button button_primary form-submit"
            type="submit"
          >
            {isEditing
              ? 'Сохранить изменения'
              : 'Добавить напиток'}
          </button>

          {isEditing && (
            <button
              className="button"
              type="button"
              onClick={onCancelEdit}
            >
              Отменить редактирование
            </button>
          )}
        </div>
      </form>
    </section>
  )
}

function DrinkCard({
  drink,
  onOpen,
  onEdit,
  onDelete,
}) {
  return (
    <article className="drink-card">
      <div className="drink-card__image">
        {drink.image ? (
          <img
            src={drink.image}
            alt={drink.name}
          />
        ) : (
          <span>{drink.name[0]}</span>
        )}
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
            {drink.available
              ? 'В наличии'
              : 'Нет в наличии'}
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
            onClick={() => onOpen(drink)}
          >
            Открыть
          </button>

          <button
            className="button"
            type="button"
            onClick={() => onEdit(drink)}
          >
            Редактировать
          </button>

          <button
            className="button button_danger"
            type="button"
            onClick={() => onDelete(drink)}
          >
            Удалить
          </button>
        </div>
      </div>
    </article>
  )
}

function DrinkList({
  drinks,
  onOpen,
  onEdit,
  onDelete,
}) {
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
          onOpen={onOpen}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  )
}

function DrinkDetails({
  drink,
  onClose,
  onEdit,
  onDelete,
}) {
  return (
    <div
      className="modal-backdrop"
      onClick={onClose}
    >
      <div
        className="modal"
        onClick={(event) => event.stopPropagation()}
      >
        <button
          className="modal__close"
          type="button"
          onClick={onClose}
        >
          ×
        </button>

        <div className="modal__image">
          {drink.image ? (
            <img
              src={drink.image}
              alt={drink.name}
            />
          ) : (
            <span>{drink.name[0]}</span>
          )}
        </div>

        <div className="modal__body">
          <div className="modal__title-row">
            <h2>{drink.name}</h2>

            <span
              className={
                drink.available
                  ? 'status status_available'
                  : 'status status_unavailable'
              }
            >
              {drink.available
                ? 'В наличии'
                : 'Нет в наличии'}
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

          <p>
            <strong>Описание:</strong> {drink.description}
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
              className="button"
              type="button"
              onClick={() => onEdit(drink)}
            >
              Редактировать
            </button>

            <button
              className="button button_danger"
              type="button"
              onClick={() => onDelete(drink)}
            >
              Удалить
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

function App() {
  const [drinks, setDrinks] = useState(getSavedDrinks)

  const [sortBy, setSortBy] = useState('newest')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [selectedTag, setSelectedTag] = useState('all')

  const [formData, setFormData] = useState(emptyFormData)
  const [errors, setErrors] = useState({})

  const [selectedDrink, setSelectedDrink] = useState(null)
  const [editingDrinkId, setEditingDrinkId] = useState(null)

  useEffect(() => {
    localStorage.setItem(
      'drink-catalog-drinks',
      JSON.stringify(drinks),
    )
  }, [drinks])

  const visibleDrinks = useMemo(() => {
    let result = [...drinks]

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
  }, [
    drinks,
    sortBy,
    selectedCategory,
    selectedTag,
  ])

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

  function handleInputChange(event) {
    const {
      name,
      value,
      type,
      checked,
      files,
    } = event.target

    if (type === 'file') {
      const file = files[0]

      if (!file) {
        return
      }

      const reader = new FileReader()

      reader.onload = () => {
        setFormData((currentData) => ({
          ...currentData,
          [name]: reader.result,
        }))
      }

      reader.readAsDataURL(file)
      return
    }

    setFormData((currentData) => ({
      ...currentData,
      [name]: type === 'checkbox' ? checked : value,
    }))

    setErrors((currentErrors) => ({
      ...currentErrors,
      [name]: '',
    }))
  }

  function validateForm(data) {
    const formErrors = {}

    if (data.name.trim().length < 3) {
      formErrors.name =
        'Название должно содержать минимум 3 символа'
    }

    if (!data.category) {
      formErrors.category = 'Выберите категорию'
    }

    if (data.type.trim().length < 3) {
      formErrors.type =
        'Тип должен содержать минимум 3 символа'
    }

    if (data.brand.trim().length < 2) {
      formErrors.brand = 'Укажите бренд'
    }

    if (data.description.trim().length < 15) {
      formErrors.description =
        'Описание должно содержать минимум 15 символов'
    }

    return formErrors
  }

  function handleSubmit(event) {
    event.preventDefault()

    const formErrors = validateForm(formData)

    if (Object.keys(formErrors).length > 0) {
      setErrors(formErrors)
      return
    }

    const drinkData = {
      name: formData.name.trim(),
      category: formData.category,
      type: formData.type.trim(),
      brand: formData.brand.trim(),
      tags: formData.tags
        .split(',')
        .map((tag) => tag.trim())
        .filter((tag) => tag.length > 0),
      description: formData.description.trim(),
      image: formData.image,
      available: formData.available,
    }

    if (editingDrinkId !== null) {
      setDrinks((currentDrinks) =>
        currentDrinks.map((drink) =>
          drink.id === editingDrinkId
            ? { ...drink, ...drinkData }
            : drink,
        ),
      )

      setEditingDrinkId(null)
    } else {
      const newDrink = {
        id: Date.now(),
        ...drinkData,
      }

      setDrinks((currentDrinks) => [
        newDrink,
        ...currentDrinks,
      ])

      setSortBy('newest')
    }

    setFormData(emptyFormData)
    setErrors({})
    setSelectedCategory('all')
    setSelectedTag('all')
  }

  function handleOpenDrink(drink) {
    setSelectedDrink(drink)
  }

  function handleEditDrink(drink) {
    setEditingDrinkId(drink.id)

    setFormData({
      name: drink.name,
      category: drink.category,
      type: drink.type,
      brand: drink.brand,
      tags: drink.tags.join(', '),
      description: drink.description,
      image: drink.image || '',
      available: drink.available,
    })

    setErrors({})
    setSelectedDrink(null)

    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    })
  }

  function handleCancelEdit() {
    setEditingDrinkId(null)
    setFormData(emptyFormData)
    setErrors({})
  }

  function handleDeleteDrink(drink) {
    const isConfirmed = window.confirm(
      `Удалить напиток «${drink.name}»?`,
    )

    if (!isConfirmed) {
      return
    }

    setDrinks((currentDrinks) =>
      currentDrinks.filter(
        (item) => item.id !== drink.id,
      ),
    )

    if (selectedDrink?.id === drink.id) {
      setSelectedDrink(null)
    }

    if (editingDrinkId === drink.id) {
      handleCancelEdit()
    }
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
          <DrinkForm
            formData={formData}
            errors={errors}
            isEditing={editingDrinkId !== null}
            onInputChange={handleInputChange}
            onSubmit={handleSubmit}
            onCancelEdit={handleCancelEdit}
          />

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

          <DrinkList
            drinks={visibleDrinks}
            onOpen={handleOpenDrink}
            onEdit={handleEditDrink}
            onDelete={handleDeleteDrink}
          />
        </section>
      </main>

      {selectedDrink && (
        <DrinkDetails
          drink={selectedDrink}
          onClose={() => setSelectedDrink(null)}
          onEdit={handleEditDrink}
          onDelete={handleDeleteDrink}
        />
      )}
    </div>
  )
}

export default App