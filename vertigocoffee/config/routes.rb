Vertigocoffee::Application.routes.draw do
  resources :posts
  root "main#index"
end
