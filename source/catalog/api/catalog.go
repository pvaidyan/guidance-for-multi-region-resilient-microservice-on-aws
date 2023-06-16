package api

import (
	"catalog/model"
	"context"
)

// CatalogAPI type
type CatalogAPI struct {
}

func (a *CatalogAPI) GetProducts(tags []string, order string, pageNum, pageSize int, ctx context.Context) ([]model.Product, error) {
	return nil, nil
}

func (a *CatalogAPI) GetProduct(id string, ctx context.Context) (*model.Product, error) {
	return nil, nil
}

func (a *CatalogAPI) GetTags(ctx context.Context) ([]model.Tag, error) {
	return nil, nil
}

func (a *CatalogAPI) GetSize(tags []string, ctx context.Context) (int, error) {
	return 0, nil
}

// NewCatalogAPI constructor
func NewCatalogAPI() (*CatalogAPI, error) {
	/*repository, err := repository.NewRepository(configuration)
	if err != nil {
		log.Println("Error creating catalog API", err)
		return nil, err
	}*/

	return &CatalogAPI{}, nil
}
